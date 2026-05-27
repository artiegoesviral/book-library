import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { DeleteResponse, User } from '../models/user.model';

@Injectable({
  providedIn: 'root',
})
export class UserService {

  private API_BASE = 'http://127.0.0.1:8000';
  private http = inject(HttpClient);

  constructor() { }

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.API_BASE}/users/`);
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(`${this.API_BASE}/users/`, user);
  }

  updateUser(user: User): Observable<User> {
    return this.http.put<User>(`${this.API_BASE}/users/${user.id}/`, user);
  }

  deleteUser(userId: number): Observable<DeleteResponse> {
    return this.http.delete<DeleteResponse>(`${this.API_BASE}/users/${userId}/`);
  }
}
