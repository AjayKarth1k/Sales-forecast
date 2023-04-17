import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ReportComponent } from './report/report.component';
import { UploadComponent } from './upload/upload.component';
import { TrendComponent } from './trend/trend.component';
import { VisualComponent } from './visual/visual.component';

const routes: Routes = [
  {path:'', component: LoginComponent},
  {path:'upload', component: UploadComponent},
  {path:'report',component: ReportComponent},
  {path:'trend',component: TrendComponent},
  {path:'visual',component: VisualComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
