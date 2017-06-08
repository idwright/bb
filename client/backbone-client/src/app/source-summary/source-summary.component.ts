import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Summary } from '../typescript-angular2-client/model/Summary';

import { ReportApi } from '../typescript-angular2-client/api/ReportApi';

@Component({
  selector: 'source-summary',
  templateUrl: './source-summary.component.html',
  styleUrls: [ './source-summary.component.css' ]
})
export class SourceSummaryComponent implements OnInit {

    summary: Summary;

    sourceName: string;

    constructor(private reportApi: ReportApi,
              private route: ActivatedRoute,
              private location: Location
              ) { 
    }

    ngOnInit(): void {
    console.log("sourcesummary");
    this.sourceName = this.route.snapshot.params['sourceId'];
      this.route.params.switchMap((params: Params) =>
        this.reportApi.getPropertiesSummary(params['sourceId'])).subscribe(
            (summary) => {
                            console.log(summary);
                            this.summary = summary;
                        },
                        (err) => console.log(err),
                        () => { console.log("Downloaded source summary") }
        );
    }


    goBack(): void {
      this.location.back();
    }

}
