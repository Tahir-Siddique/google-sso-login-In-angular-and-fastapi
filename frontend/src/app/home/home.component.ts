import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  username: string = '';
  roles: string[] = [];

  constructor(
    private http: HttpClient,
    private router: Router,
    private cookieService: CookieService
  ) {}

  ngOnInit() {
    this.http.get<{ username: string, roles: string[] }>('http://localhost:8000/user/me')
      .subscribe(data => {
        this.username = data.username;
        this.roles = data.roles;
      });
  }

  logout() {
    this.cookieService.delete('access_token');
    this.router.navigate(['/']);
  }
}
