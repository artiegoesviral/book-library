import { Routes } from '@angular/router';

import { LoginComponent } from './pages/login/login';
import { RegisterComponent } from './pages/register/register';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { PublicProfileComponent } from './pages/public-profile/public-profile';

import { authGuard } from './guards/auth.guard';

export const routes: Routes = [

    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },

    {
        path: 'login',
        component: LoginComponent
    },

    {
        path: 'register',
        component: RegisterComponent
    },

    // PRIVATE ROUTE
    {
        path: 'dashboard',
        component: DashboardComponent,
        canActivate: [authGuard]
    },

    {
        path: 'user/:username',
        component: PublicProfileComponent,
    },

    {
        path: '**',
        redirectTo: 'login'
    }
];