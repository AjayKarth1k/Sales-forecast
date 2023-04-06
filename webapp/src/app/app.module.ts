import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { LoginComponent } from './login/login.component';
import { ReportComponent } from './report/report.component';
import { RouterModule, Router } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { TrendComponent } from './trend/trend.component';
import { VisualComponent } from './visual/visual.component';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ReportComponent,
    UploadComponent,
    TrendComponent,
    VisualComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    RouterModule.forRoot([
      { path: 'upload', component: UploadComponent },
      { path: 'report', component: ReportComponent }
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
