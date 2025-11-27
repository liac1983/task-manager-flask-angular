import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:5000';
  private tokenKey = 'task_manager_token';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http
      .post<{ access_token: string }>(`${this.apiUrl}/login`, {
        username,
        password,
      })
      .pipe(
        tap((res) => {
          localStorage.setItem(this.tokenKey, res.access_token);
        })
      );
  }

  // 👉 NOVO
  register(username: string, email: string, password: string) {
    return this.http.post<{ msg: string }>(`${this.apiUrl}/register`, {
      username,
      email,
      password,
    });
  }

  logout() {
    localStorage.removeItem(this.tokenKey);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
