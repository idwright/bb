import { Component, OnInit } from '@angular/core';

import { Summary } from './typescript-angular2-client/model/Summary';

import { ReportApi } from './typescript-angular2-client/api/ReportApi';

@Component({
  selector: 'my-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {

  summary: Summary;

  constructor(private reportApi: ReportApi) { }

  ngOnInit(): void {
    this.reportApi.getSummary()
    .subscribe(
    (summary) => {
                    console.log(summary);
                    this.summary = summary;
                },
                (err) => console.log(err),
                () => { console.log("Downloaded summary") }
                );
  }
}
