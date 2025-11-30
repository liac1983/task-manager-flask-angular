import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { Observable } from 'rxjs';

export interface Task {
  id?: number;
  title: string;
  description?: string;
  done?: boolean;
  category?: 'work' | 'study' | 'personal' | 'other'; 
}

@Injectable({ providedIn: 'root' })
export class TaskService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient, private auth: AuthService) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.auth.getToken();
    return new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
  }

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.apiUrl}/tasks`, {
      headers: this.getAuthHeaders()
    });
  }

  createTask(task: Task): Observable<any> {
    return this.http.post(`${this.apiUrl}/tasks`, task, {
      headers: this.getAuthHeaders()
    });
  }

  updateTask(task: Task): Observable<any> {
    return this.http.put(`${this.apiUrl}/tasks/${task.id}`, task, {
      headers: this.getAuthHeaders()
    });
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/tasks/${id}`, {
      headers: this.getAuthHeaders()
    });
  }
}
