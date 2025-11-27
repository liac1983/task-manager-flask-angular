import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TaskService, Task } from '../task.service';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.scss'],
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  newTask: Task = { title: '', description: '', done: false };
  editingTask: Task | null = null;

  constructor(
    private taskService: TaskService,
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadTasks();
  }

  loadTasks() {
    this.taskService.getTasks().subscribe((tasks) => (this.tasks = tasks));
  }

  addTask() {
    this.taskService.createTask(this.newTask).subscribe(() => {
      this.newTask = { title: '', description: '', done: false };
      this.loadTasks();
    });
  }

  startEdit(task: Task) {
    this.editingTask = { ...task };
  }

  saveEdit() {
    if (!this.editingTask) return;
    this.taskService.updateTask(this.editingTask).subscribe(() => {
      this.editingTask = null;
      this.loadTasks();
    });
  }

  deleteTask(id: number | undefined) {
    if (id === undefined) return;

    const confirmed = confirm('Are you sure you want to delete this task?');

    if (!confirmed) {
      return;
    }

    this.taskService.deleteTask(id).subscribe(() => this.loadTasks());
  }


  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
