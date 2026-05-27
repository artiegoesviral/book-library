import { Component, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { RouterLink, Router } from "@angular/router";
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth.service';
import { ReactiveFormsModule, FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-admin-dashboard',
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule]
})

export class DashboardComponent {

  constructor(
    private auth: AuthService,
    private router: Router
  ) { }

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }


  selectedType = 'book';

  formats = ['physical', 'ebook', 'audiobook'];

  form = new FormGroup({
    title: new FormControl(''),
    author: new FormControl(''),
    genre: new FormControl(''),
    format: new FormControl('physical'),
    read: new FormControl(false),
  });

  items: any[] = [];

  setType(type: 'book' | 'comic') {
    this.selectedType = type;
  }

  submit() {
    const newItem = {
      ...this.form.value,
      media_type: this.selectedType
    };
    console.log(newItem);
  }
}