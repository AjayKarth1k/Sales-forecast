import { Component } from '@angular/core';
import { HttpClient, HttpEventType, HttpResponse } from '@angular/common/http';
import { Router } from '@angular/router';

interface UploadResponse {
  success: Boolean;
}

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  showWarning = false;
  uploadProgress = 0;
  periodicityOptions = ['Days', 'Weeks', 'Months', 'Years'];
  numerixOptions: string[] = [];
  selectedPeriodicity: string | null = null;
  selectedNumerix: number | null = null;

  constructor(private http: HttpClient, private router: Router) {}

  uploadFile() {
    const fileUpload = document.getElementById('file-upload') as HTMLInputElement | null;

    if (!fileUpload) {
      return; // null values to file upload when no file is given
    }

    const file = fileUpload.files?.[0]; // use optional chaining to safely access files array

    if (!file || (file.type !== 'text/csv' && file.type !== 'application/vnd.ms-excel' && file.type !== 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
      this.showWarning = true;
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('selectedNumerix', this.selectedNumerix?.toString() ?? '');
    formData.append('selectedPeriodicity', this.selectedPeriodicity ?? '');

    this.http.post('http://127.0.0.1:5000/upload', formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe((event) => {
      if (event.type === HttpEventType.UploadProgress) {
        const progress = Math.round((100 * event.loaded) / (event.total ?? 1));
        this.uploadProgress = progress;
      } else if (event instanceof HttpResponse) {
        const response = event.body as UploadResponse;
        console.log(response);
          this.router.navigate(['/report']);
      }
    });
  }

  isUploadEnabled(): boolean {
    return !!this.selectedPeriodicity && !!this.selectedNumerix;
  }

  onPeriodicityChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const periodicity = target.value;

    if (periodicity === 'Days') {
      this.numerixOptions = Array.from({length: 31}, (_, i) => (i + 1).toString());
    } else if (periodicity === 'Weeks') {
      this.numerixOptions = Array.from({length: 4}, (_, i) => (i + 1).toString());
    }else if (periodicity === 'Months') {
      this.numerixOptions = Array.from({length: 12}, (_, i) => (i + 1).toString());
    } else if (periodicity === 'Years') {
      this.numerixOptions = Array.from({length: 10}, (_, i) => (i + 1).toString());
    }

    this.selectedPeriodicity = periodicity;
  }

  onNumerixChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const numerix = parseInt(target.value);

    this.selectedNumerix = numerix;
  }
}
