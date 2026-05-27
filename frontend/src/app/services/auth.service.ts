import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  register(username: string, email: string, password: string) {
    return this.http.post<any>(`${this.apiUrl}/register`, {
      username,
      email,
      password
    }).pipe(
      tap(res => {
        localStorage.setItem('token', res.access_token);
      })
    );
  }

  login(email: string, password: string) {
    return this.http.post<any>(`${this.apiUrl}/login`, {
      email,
      password
    }).pipe(
      tap(res => {
        localStorage.setItem('token', res.access_token);
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