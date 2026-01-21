"""
Tests for TaskService.
"""

import pytest
from todo.domain.errors import TaskNotFoundError, ValidationError
from todo.domain.value_objects import Priority, TaskStatus


class TestCreateTask:
    """Tests for TaskService.create_task()."""

    def test_create_task_with_title(self, service):
        """create_task() should create task with title."""
        task = service.create_task("Test task")
        assert task.title == "Test task"

    def test_create_task_assigns_id(self, service):
        """create_task() should assign unique id."""
        task1 = service.create_task("Task 1")
        task2 = service.create_task("Task 2")
        assert task1.id == 1
        assert task2.id == 2

    def test_create_task_with_description(self, service):
        """create_task() should accept description."""
        task = service.create_task("Test", description="A description")
        assert task.description == "A description"

    def test_create_task_strips_title(self, service):
        """create_task() should strip whitespace from title."""
        task = service.create_task("  Test task  ")
        assert task.title == "Test task"

    def test_create_task_strips_description(self, service):
        """create_task() should strip whitespace from description."""
        task = service.create_task("Test", description="  Description  ")
        assert task.description == "Description"

    def test_create_task_with_priority(self, service):
        """create_task() should accept priority."""
        task = service.create_task("Test", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_create_task_default_priority_is_medium(self, service):
        """create_task() should default to MEDIUM priority."""
        task = service.create_task("Test")
        assert task.priority == Priority.MEDIUM

    def test_create_task_with_tags(self, service):
        """create_task() should accept tags."""
        task = service.create_task("Test", tags=["work", "urgent"])
        assert "work" in task.tags
        assert "urgent" in task.tags

    def test_create_task_normalizes_tags(self, service):
        """create_task() should normalize tags to lowercase."""
        task = service.create_task("Test", tags=["WORK", "Urgent"])
        assert "work" in task.tags
        assert "urgent" in task.tags

    def test_create_task_empty_title_raises_error(self, service):
        """create_task() should raise ValidationError for empty title."""
        with pytest.raises(ValidationError) as exc_info:
            service.create_task("")
        assert "empty" in str(exc_info.value).lower()

    def test_create_task_whitespace_title_raises_error(self, service):
        """create_task() should raise ValidationError for whitespace-only title."""
        with pytest.raises(ValidationError):
            service.create_task("   ")

    def test_create_task_long_title_raises_error(self, service):
        """create_task() should raise ValidationError for title > 200 chars."""
        with pytest.raises(ValidationError) as exc_info:
            service.create_task("x" * 201)
        assert "200" in str(exc_info.value)

    def test_create_task_long_description_raises_error(self, service):
        """create_task() should raise ValidationError for description > 2000 chars."""
        with pytest.raises(ValidationError) as exc_info:
            service.create_task("Test", description="x" * 2001)
        assert "2000" in str(exc_info.value)

    def test_create_task_empty_tag_raises_error(self, service):
        """create_task() should raise ValidationError for empty tag."""
        with pytest.raises(ValidationError):
            service.create_task("Test", tags=[""])

    def test_create_task_long_tag_raises_error(self, service):
        """create_task() should raise ValidationError for tag > 50 chars."""
        with pytest.raises(ValidationError) as exc_info:
            service.create_task("Test", tags=["x" * 51])
        assert "50" in str(exc_info.value)

    def test_create_task_duplicate_tags_raises_error(self, service):
        """create_task() should raise ValidationError for duplicate tags."""
        with pytest.raises(ValidationError) as exc_info:
            service.create_task("Test", tags=["work", "work"])
        assert "duplicate" in str(exc_info.value).lower()


class TestGetTask:
    """Tests for TaskService.get_task()."""

    def test_get_task_returns_task(self, service, sample_task):
        """get_task() should return task with matching id."""
        result = service.get_task(sample_task.id)
        assert result.id == sample_task.id

    def test_get_task_not_found_raises_error(self, service):
        """get_task() should raise TaskNotFoundError for missing id."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            service.get_task(999)
        assert exc_info.value.task_id == 999


class TestGetAllTasks:
    """Tests for TaskService.get_all_tasks()."""

    def test_get_all_tasks_empty_list(self, service):
        """get_all_tasks() should return empty list initially."""
        assert service.get_all_tasks() == []

    def test_get_all_tasks_returns_all(self, service, multiple_tasks):
        """get_all_tasks() should return all tasks."""
        result = service.get_all_tasks()
        assert len(result) == 3

    def test_get_all_tasks_sorted_by_id(self, service, multiple_tasks):
        """get_all_tasks() should return tasks sorted by id."""
        result = service.get_all_tasks()
        ids = [t.id for t in result]
        assert ids == sorted(ids)


class TestMarkTaskComplete:
    """Tests for TaskService.mark_task_complete()."""

    def test_mark_complete_changes_status(self, service, sample_task):
        """mark_task_complete() should change status to COMPLETED."""
        service.mark_task_complete(sample_task.id)
        task = service.get_task(sample_task.id)
        assert task.status == TaskStatus.COMPLETED

    def test_mark_complete_returns_task(self, service, sample_task):
        """mark_task_complete() should return the updated task."""
        result = service.mark_task_complete(sample_task.id)
        assert result.status == TaskStatus.COMPLETED

    def test_mark_complete_not_found_raises_error(self, service):
        """mark_task_complete() should raise TaskNotFoundError for missing id."""
        with pytest.raises(TaskNotFoundError):
            service.mark_task_complete(999)


class TestMarkTaskIncomplete:
    """Tests for TaskService.mark_task_incomplete()."""

    def test_mark_incomplete_changes_status(self, service, sample_task):
        """mark_task_incomplete() should change status to PENDING."""
        service.mark_task_complete(sample_task.id)
        service.mark_task_incomplete(sample_task.id)
        task = service.get_task(sample_task.id)
        assert task.status == TaskStatus.PENDING

    def test_mark_incomplete_returns_task(self, service, sample_task):
        """mark_task_incomplete() should return the updated task."""
        service.mark_task_complete(sample_task.id)
        result = service.mark_task_incomplete(sample_task.id)
        assert result.status == TaskStatus.PENDING


class TestUpdateTaskTitle:
    """Tests for TaskService.update_task_title()."""

    def test_update_title_changes_title(self, service, sample_task):
        """update_task_title() should change the title."""
        service.update_task_title(sample_task.id, "New title")
        task = service.get_task(sample_task.id)
        assert task.title == "New title"

    def test_update_title_strips_whitespace(self, service, sample_task):
        """update_task_title() should strip whitespace."""
        service.update_task_title(sample_task.id, "  New title  ")
        task = service.get_task(sample_task.id)
        assert task.title == "New title"

    def test_update_title_empty_raises_error(self, service, sample_task):
        """update_task_title() should raise ValidationError for empty title."""
        with pytest.raises(ValidationError):
            service.update_task_title(sample_task.id, "")

    def test_update_title_long_raises_error(self, service, sample_task):
        """update_task_title() should raise ValidationError for title > 200 chars."""
        with pytest.raises(ValidationError):
            service.update_task_title(sample_task.id, "x" * 201)


class TestUpdateTaskDescription:
    """Tests for TaskService.update_task_description()."""

    def test_update_description_changes_description(self, service, sample_task):
        """update_task_description() should change the description."""
        service.update_task_description(sample_task.id, "New description")
        task = service.get_task(sample_task.id)
        assert task.description == "New description"

    def test_update_description_can_set_none(self, service, sample_task):
        """update_task_description() should allow setting to None."""
        service.update_task_description(sample_task.id, None)
        task = service.get_task(sample_task.id)
        assert task.description is None

    def test_update_description_long_raises_error(self, service, sample_task):
        """update_task_description() should raise ValidationError for > 2000 chars."""
        with pytest.raises(ValidationError):
            service.update_task_description(sample_task.id, "x" * 2001)


class TestUpdateTaskPriority:
    """Tests for TaskService.update_task_priority()."""

    def test_update_priority_changes_priority(self, service, sample_task):
        """update_task_priority() should change the priority."""
        service.update_task_priority(sample_task.id, Priority.HIGH)
        task = service.get_task(sample_task.id)
        assert task.priority == Priority.HIGH


class TestTaskTags:
    """Tests for TaskService tag operations."""

    def test_add_tag_adds_tag(self, service, sample_task):
        """add_task_tag() should add a tag to the task."""
        service.add_task_tag(sample_task.id, "work")
        task = service.get_task(sample_task.id)
        assert "work" in task.tags

    def test_add_tag_normalizes(self, service, sample_task):
        """add_task_tag() should normalize tag to lowercase."""
        service.add_task_tag(sample_task.id, "WORK")
        task = service.get_task(sample_task.id)
        assert "work" in task.tags

    def test_add_tag_empty_raises_error(self, service, sample_task):
        """add_task_tag() should raise ValidationError for empty tag."""
        with pytest.raises(ValidationError):
            service.add_task_tag(sample_task.id, "")

    def test_add_tag_long_raises_error(self, service, sample_task):
        """add_task_tag() should raise ValidationError for tag > 50 chars."""
        with pytest.raises(ValidationError):
            service.add_task_tag(sample_task.id, "x" * 51)

    def test_add_tag_duplicate_raises_error(self, service, sample_task):
        """add_task_tag() should raise ValidationError for duplicate tag."""
        service.add_task_tag(sample_task.id, "work")
        with pytest.raises(ValidationError) as exc_info:
            service.add_task_tag(sample_task.id, "work")
        assert "already exists" in str(exc_info.value)

    def test_remove_tag_removes_tag(self, service, sample_task):
        """remove_task_tag() should remove a tag from the task."""
        service.add_task_tag(sample_task.id, "work")
        service.remove_task_tag(sample_task.id, "work")
        task = service.get_task(sample_task.id)
        assert "work" not in task.tags

    def test_remove_tag_not_found_raises_error(self, service, sample_task):
        """remove_task_tag() should raise ValidationError for missing tag."""
        with pytest.raises(ValidationError) as exc_info:
            service.remove_task_tag(sample_task.id, "nonexistent")
        assert "not found" in str(exc_info.value)


class TestSearchTasks:
    """Tests for TaskService.search_tasks()."""

    def test_search_by_title_keyword(self, service, multiple_tasks):
        """search_tasks() should find tasks matching keyword in title."""
        results = service.search_tasks("First")
        assert len(results) == 1
        assert results[0].title == "First task"

    def test_search_by_description_keyword(self, service, multiple_tasks):
        """search_tasks() should find tasks matching keyword in description."""
        results = service.search_tasks("description")
        assert len(results) == 1
        assert results[0].title == "Second task"

    def test_search_case_insensitive(self, service, multiple_tasks):
        """search_tasks() should be case-insensitive."""
        results = service.search_tasks("FIRST")
        assert len(results) == 1

    def test_search_with_status_filter(self, service, multiple_tasks):
        """search_tasks() should filter by status."""
        service.mark_task_complete(multiple_tasks[0].id)
        results = service.search_tasks("task", status=TaskStatus.COMPLETED)
        assert len(results) == 1
        assert results[0].id == multiple_tasks[0].id

    def test_search_with_priority_filter(self, service, multiple_tasks):
        """search_tasks() should filter by priority."""
        results = service.search_tasks("task", priority=Priority.HIGH)
        assert len(results) == 1
        assert results[0].priority == Priority.HIGH

    def test_search_with_tag_filter(self, service, multiple_tasks):
        """search_tasks() should filter by tag."""
        results = service.search_tasks("task", tag="urgent")
        assert len(results) == 1


class TestFilterTasks:
    """Tests for TaskService.filter_tasks()."""

    def test_filter_by_status(self, service, multiple_tasks):
        """filter_tasks() should filter by status."""
        service.mark_task_complete(multiple_tasks[0].id)
        results = service.filter_tasks(status=TaskStatus.COMPLETED)
        assert len(results) == 1
        assert results[0].status == TaskStatus.COMPLETED

    def test_filter_by_priority(self, service, multiple_tasks):
        """filter_tasks() should filter by priority."""
        results = service.filter_tasks(priority=Priority.LOW)
        assert len(results) == 1
        assert results[0].priority == Priority.LOW

    def test_filter_by_tag(self, service, multiple_tasks):
        """filter_tasks() should filter by tag."""
        results = service.filter_tasks(tag="work")
        assert len(results) == 1

    def test_filter_no_criteria_returns_all(self, service, multiple_tasks):
        """filter_tasks() with no criteria should return all tasks."""
        results = service.filter_tasks()
        assert len(results) == 3

    def test_filter_multiple_criteria(self, service, multiple_tasks):
        """filter_tasks() should AND multiple criteria."""
        results = service.filter_tasks(priority=Priority.HIGH, tag="urgent")
        assert len(results) == 1


class TestSortTasks:
    """Tests for TaskService.sort_tasks()."""

    def test_sort_by_id(self, service, multiple_tasks):
        """sort_tasks() should sort by id."""
        results = service.sort_tasks(multiple_tasks, field="id")
        ids = [t.id for t in results]
        assert ids == sorted(ids)

    def test_sort_by_id_reverse(self, service, multiple_tasks):
        """sort_tasks() should sort by id in reverse."""
        results = service.sort_tasks(multiple_tasks, field="id", reverse=True)
        ids = [t.id for t in results]
        assert ids == sorted(ids, reverse=True)

    def test_sort_by_title(self, service, multiple_tasks):
        """sort_tasks() should sort by title."""
        results = service.sort_tasks(multiple_tasks, field="title")
        titles = [t.title for t in results]
        assert titles == sorted(titles, key=str.lower)

    def test_sort_by_priority(self, service, multiple_tasks):
        """sort_tasks() should sort by priority (high first)."""
        results = service.sort_tasks(multiple_tasks, field="priority")
        priorities = [t.priority for t in results]
        assert priorities[0] == Priority.HIGH
        assert priorities[-1] == Priority.LOW

    def test_sort_by_created(self, service, multiple_tasks):
        """sort_tasks() should sort by created_at."""
        results = service.sort_tasks(multiple_tasks, field="created")
        dates = [t.created_at for t in results]
        assert dates == sorted(dates)

    def test_sort_invalid_field_raises_error(self, service, multiple_tasks):
        """sort_tasks() should raise ValidationError for invalid field."""
        with pytest.raises(ValidationError) as exc_info:
            service.sort_tasks(multiple_tasks, field="invalid")
        assert "invalid" in str(exc_info.value).lower()


class TestDeleteTask:
    """Tests for TaskService.delete_task()."""

    def test_delete_task_removes_task(self, service, sample_task):
        """delete_task() should remove the task."""
        service.delete_task(sample_task.id)
        with pytest.raises(TaskNotFoundError):
            service.get_task(sample_task.id)

    def test_delete_task_returns_true(self, service, sample_task):
        """delete_task() should return True on success."""
        result = service.delete_task(sample_task.id)
        assert result is True

    def test_delete_task_not_found_raises_error(self, service):
        """delete_task() should raise TaskNotFoundError for missing id."""
        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)
