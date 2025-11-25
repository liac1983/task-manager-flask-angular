import { Routes } from '@angular/router';
import { LoginComponent } from './auth/login/login.component';
import { TaskListComponent } from './tasks/task-list/task-list.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'tasks', component: TaskListComponent, canActivate: [AuthGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' }
];
