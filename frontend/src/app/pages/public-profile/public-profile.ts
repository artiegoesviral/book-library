import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-public-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './public-profile.html',
  styleUrls: ['./public-profile.css']
})
export class PublicProfileComponent {

  username = '';
  items: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient
  ) {
    this.route.params.subscribe(params => {
      this.username = params['username'];
      this.loadLibrary();
    });
  }

  loadLibrary() {
    this.http.get<any[]>(
      `http://127.0.0.1:8000/users/${this.username}/library`
    ).subscribe(data => {
      this.items = data;
    });
  }
}
