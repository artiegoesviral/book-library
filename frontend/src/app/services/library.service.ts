import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class LibraryService {

  private apiUrl = 'http://127.0.0.1:8000/items';
  http: any;
  items: any;

  constructor(private libraryService: LibraryService) {
    this.loadItems();
  }

  loadItems() {
    this.libraryService.getMyItems().subscribe((items: any) => {
      this.items = items;
    });
  }

  getMyItems() {
    return this.http.get(this.apiUrl + '/me');
  }

  getUserItems(username: string) {
    return this.http.get(
      `${this.apiUrl}/user/${username}`
    );
  }

  create(item: any) {
    return this.http.post(
      this.apiUrl + '/',
      item
    );
  }

  delete(id: number) {
    return this.http.delete(
      `${this.apiUrl}/${id}`
    );
  }
}