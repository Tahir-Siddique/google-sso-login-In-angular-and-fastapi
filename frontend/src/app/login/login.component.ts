import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { faGoogle } from '@fortawesome/free-brands-svg-icons';
import { FaIconLibrary, FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl:'./login.component.css',
  standalone: true,
  imports: [MatButtonModule, FontAwesomeModule]
})
export class LoginComponent implements OnInit {
  faGoogle = faGoogle;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private cookieService: CookieService,
    private library: FaIconLibrary
  ) {
    library.addIcons(faGoogle);
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const token = params['token'];
      if (token) {
        this.cookieService.set('access_token', token);
        this.router.navigate(['/home']);
      }
    });
  }

  login() {
    window.location.href = 'http://localhost:8000/login/google';
  }
}
