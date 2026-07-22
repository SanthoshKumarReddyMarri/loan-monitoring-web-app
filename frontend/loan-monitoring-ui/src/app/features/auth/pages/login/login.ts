
import { AuthService } from '../../services/auth';
import { AfterViewInit, Component } from '@angular/core';

declare const google: any;

@Component({
  selector: 'app-login',
  imports: [],
  templateUrl: './login.html',
  styleUrl: './login.css'
})

export class Login implements AfterViewInit {

  constructor(
    private authService: AuthService
  ) {}

  ngAfterViewInit(): void {


    console.log('Client ID:', '843479024809-du79gv73isame0qbiu0kebu6e2m8b1lo.apps.googleusercontent.com');

    google.accounts.id.initialize({
      client_id: '843479024809-du79gv73isame0qbiu0kebu6e2m8b1lo.apps.googleusercontent.com',
      // callback: (response: any) => {
      //   console.log(response);
      // }
      callback: (response: any) => {

      this.authService.login(response.credential).subscribe({

        next: (backendResponse) => {
          console.log('Backend Response');
          console.log(backendResponse);
        },

        error: (error) => {
          console.error('Backend Error');
          console.error(error);
        }

      });

}
    });

    google.accounts.id.renderButton(
      document.getElementById("google-button"),
      {
        theme: "outline",
        size: "large",
        width: 250
      }
    );

  }

  // login(): void {
  //   this.authService.login().subscribe({
  //     next: (response) => {
  //       console.log('Login Successful');
  //       console.log(response);
  //     },
  //     error: (error) => {
  //       console.error('Login Failed');
  //       console.error(error);
  //     }
  //   });
  // }

}