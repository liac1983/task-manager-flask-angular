import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent {
  username = '';
  email = '';
  password = '';
  message = '';
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  onSubmit() {
    this.error = '';
    this.message = '';
    this.auth.register(this.username, this.email, this.password).subscribe({
      next: () => {
        this.message = 'Registration successful. You can now log in.';
        
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.error =
          err.error?.msg || 'Error registering. Try a different username/email.';
      },
    });
  }
}
