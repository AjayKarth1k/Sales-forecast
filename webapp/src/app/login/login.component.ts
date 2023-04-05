import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private router: Router) {}

  login() {
    if (this.username === 'Ajay' && this.password === '12345') {
      // Navigate to home page
      this.router.navigate(['/upload']);
    } else {
      this.errorMessage = 'Invalid credentials';
    }
  }
}
