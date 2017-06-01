import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Summary } from './typescript-angular2-client/model/Summary';

import { ReportApi } from './typescript-angular2-client/api/ReportApi';

@Component({
  selector: 'source-property-summary',
  templateUrl: './source-property-summary.component.html',
  styleUrls: [ './source-property-summary.component.css' ]
})
export class SourcePropertySummaryComponent implements OnInit {

    summary: Summary;

    sourceName: string;
    propertyName: string;

    constructor(private reportApi: ReportApi,
              private route: ActivatedRoute,
              private location: Location
              ) { 
    }

    ngOnInit(): void {
        console.log("source property summary");
        this.sourceName = this.route.snapshot.params['sourceId'];
        this.propertyName = this.route.snapshot.params['propertyName'];

      this.route.params.switchMap((params: Params) =>
        this.reportApi.getPropertyValuesSummary(params['sourceId'], params['propertyName'], 0)).subscribe(
            (summary) => {
                            console.log(summary);
                            this.summary = summary;
                        },
                        (err) => console.log(err),
                        () => { console.log("Downloaded source property summary") }
        );
    }


    goBack(): void {
      this.location.back();
    }

}
