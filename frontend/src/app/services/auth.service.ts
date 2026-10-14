import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'https://book-library-g1es.onrender.com';

  constructor(private http: HttpClient) { }

  register(username: string, email: string, password: string) {
    return this.http.post<{ message: string; user_id: number; }>(`${this.apiUrl}/register`, {
      username,
      email,
      password
    });
  }

  login(email: string, password: string) {
    return this.http.post<{ access_token: string; tokentype: string; user: { id: number; username: string; email: string; } }>(`${this.apiUrl}/login`, {
      email,
      password
    }).pipe(
      tap(res => {
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('username', res.user.username);
      })
    );
  }

  logout() {
    localStorage.removeItem('token');
  }

  isLogged() {
    return !!localStorage.getItem('token');
  }
}