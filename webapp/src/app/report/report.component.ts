import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as Papa from 'papaparse';
import { Router } from '@angular/router';


@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit{
  constructor(private http: HttpClient,
    private router: Router){}
    public displayImage: boolean = false;
    headers?: string[] = [];
    rows: any[] = [];
    ngOnInit(): void {
  
      this.http.get('assets\\Predicted_result.csv', { responseType: 'text' })
        .subscribe((response: string) => {
          const csv = response;
          const results = Papa.parse(csv, { header: true });
          this.headers = results.meta.fields;
          this.rows = results.data;
        }
        );

    }
  

  showImage() {
    this.displayImage = true;
  }

  hideImage() {
    this.displayImage = false;
  }
}
