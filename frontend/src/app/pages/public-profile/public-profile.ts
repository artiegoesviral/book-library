import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

type LibraryFilter = 'all' | 'book' | 'comic' | 'currently';

@Component({
  selector: 'app-public-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './public-profile.html',
  styleUrls: ['./public-profile.css']
})
export class PublicProfileComponent implements OnInit {

  username = '';
  libraryItems: any[] = [];
  loading = true;
  userNotFound = false;

  selectedType: LibraryFilter = 'all';
  sortField = '';

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.username = params['username'];
      this.selectedType = 'all';
      this.sortField = '';

      this.resetState();
      this.loadLibrary();
    });
  }

  resetState(): void {
    this.loading = true;
    this.userNotFound = false;
    this.libraryItems = [];
  }

  loadLibrary(): void {
    this.loading = true;
    this.userNotFound = false;

    this.http.get<any[]>(
      `https://book-library-g1es.onrender.com/items/user/${encodeURIComponent(this.username)}`
    ).subscribe({
      next: (data) => {
        this.libraryItems = data ?? [];
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Load public library error:', err);
        this.loading = false;
        this.userNotFound = err.status === 404;
        this.cdr.detectChanges();
      }
    });
  }

  setType(type: LibraryFilter): void {
    this.selectedType = type;
  }

  get filteredItems(): any[] {
    let result = [...this.libraryItems];

    if (this.selectedType === 'currently') {
      result = result.filter(item => item.currently === true);
    } else if (this.selectedType === 'book' || this.selectedType === 'comic') {
      result = result.filter(item => item.media_type === this.selectedType);
    }

    if (this.sortField) {
      const field = this.sortField;

      result.sort((a, b) =>
        String(a[field] ?? '').localeCompare(String(b[field] ?? ''))
      );
    }

    return result;
  }

  sortItems(field: string): void {
    this.sortField = field;
  }

  navigateToDashboard(): void {
    this.router.navigate(['/book-library/dashboard']);
  }
}