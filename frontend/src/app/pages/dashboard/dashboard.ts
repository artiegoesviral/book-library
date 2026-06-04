import { ChangeDetectorRef, Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormControl, FormGroup } from '@angular/forms';

import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})
export class DashboardComponent {

  selectedType: 'book' | 'comic' | 'all' = 'all';

  items: any[] = [];

  formats = ['physical', 'ebook', 'audiobook'];

  editingId: number | null = null;

  sortField: 'title' | 'author' | 'genre' | 'language' | '' = '';

  form = new FormGroup({
    title: new FormControl(''),
    author: new FormControl(''),
    genre: new FormControl(''),
    language: new FormControl(''),
    format: new FormControl('physical'),
    read: new FormControl(false),
    media_type: new FormControl('book')
  });

  constructor(
    private auth: AuthService,
    private router: Router,
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) {
    this.loadItems('book');
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }

  setType(type: 'all' | 'book' | 'comic') {

    this.selectedType = type;

    this.loadItems(this.selectedType);
  }

  clearFilter() {
    this.selectedType = 'all';
    this.loadItems(this.selectedType);
  }

  loadItems(type: 'all' | 'book' | 'comic' = this.selectedType) {

    let url = 'https://book-library-g1es.onrender.com/items/me';

    if (type !== 'all') {
      url += `?media_type=${type}`;
    }

    this.http.get<any[]>(url).subscribe({
      next: (data) => {

        this.items = data ?? [];

        if (this.sortField) {
          this.sortItems(this.sortField);
        }

        this.cdr.detectChanges();
      },

      error: (err) => {
        console.error('Load items error:', err);
      }
    });
  }

  submit() {

    if (this.editingId !== null) {
      this.updateItem();
      return;
    }

    const newItem = {
      title: this.form.value.title ?? '',
      author: this.form.value.author ?? '',
      genre: this.form.value.genre ?? '',
      language: this.form.value.language ?? '',
      format: this.form.value.format ?? 'physical',
      read: this.form.value.read ?? false,
      media_type: this.form.value.media_type ?? 'book'
    };

    this.http.post(
      'https://book-library-g1es.onrender.com/items/',
      newItem
    ).subscribe({
      next: () => {

        this.form.reset({
          format: 'physical',
          read: false
        });

        this.loadItems(this.selectedType);
      },
      error: (err) => {
        console.error('Create item error:', err);
      }
    });
  }

  deleteItem(id: number) {
    this.http.delete(
      `https://book-library-g1es.onrender.com/items/${id}`
    ).subscribe({
      next: () => {
        this.loadItems(this.selectedType);
      },
      error: (err) => {
        console.error('Delete error:', err);
      }
    });
  }

  startEdit(item: any) {

    this.editingId = item.id;

    this.form.patchValue({
      title: item.title,
      author: item.author,
      genre: item.genre,
      language: item.language,
      format: item.format,
      read: item.read,
      media_type: item.media_type
    });
  }

  cancelEdit() {
    this.editingId = null;

    this.form.reset({
      format: 'physical',
      read: false,
      media_type: 'book'
    });
  }

  updateItem() {

    if (this.editingId === null) {
      return;
    }

    const updatedItem = {
      title: this.form.value.title ?? '',
      author: this.form.value.author ?? '',
      genre: this.form.value.genre ?? '',
      language: this.form.value.language ?? '',
      format: this.form.value.format ?? 'physical',
      read: this.form.value.read ?? false,
      media_type: this.form.value.media_type ?? 'book'
    };

    this.http.put(
      `https://book-library-g1es.onrender.com/items/${this.editingId}`,
      updatedItem
    ).subscribe({
      next: () => {

        this.editingId = null;

        this.form.reset({
          format: 'physical',
          read: false
        });

        this.loadItems(this.selectedType);
      },
      error: (err) => {
        console.error('Update error:', err);
      }
    });
  }

  sortItems(field: string) {

    this.items = [...this.items].sort((a, b) =>
      (a[field] || '').localeCompare(b[field] || '')
    );

    this.cdr.detectChanges();
  }
}