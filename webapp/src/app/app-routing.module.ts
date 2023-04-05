import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ReportComponent } from './report/report.component';
import { UploadComponent } from './upload/upload.component';

const routes: Routes = [
  {path:'', component: LoginComponent},
  {path:'upload', component: UploadComponent},
  {path:'report',component: ReportComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
