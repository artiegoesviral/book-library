import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ChangeDetectorRef } from '@angular/core';

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

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.username = params['username'];

      this.resetState();
      this.loadLibrary();
    });
  }

  resetState(): void {
    this.loading = true;
    this.userNotFound = false;
    this.libraryItems = [];
  }

  debugId = Math.random();

  loadLibrary(): void {
    this.loading = true;

    this.userNotFound = false;

    this.http.get<any[]>(
      `https://book-library-g1es.onrender.com/items/user/${this.username}`
    ).subscribe({
      next: (data: any[]) => {
        this.libraryItems = data;
        this.loading = false;

        this.cdr.detectChanges(); //
      },
      error: (err) => {
        console.log("ERROR STATUS:", err.status);
        this.loading = false;

        if (err.status === 404) {
          console.log("userNotFound =", this.userNotFound);
          console.log("loading =", this.loading);
          this.userNotFound = true;
        }

        console.log(err);
      }
    });
  }

  sortItems(field: string) {

    this.libraryItems = [...this.libraryItems].sort((a, b) =>
      (a[field] || '').localeCompare(b[field] || '')
    );

    this.cdr.detectChanges();
  }
}