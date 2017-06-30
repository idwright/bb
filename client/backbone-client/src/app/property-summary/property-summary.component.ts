import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';

import { Summary } from '../typescript-angular2-client/model/Summary';

import { ReportApi } from '../typescript-angular2-client/api/ReportApi';

@Component({
  selector: 'app-property-summary',
  providers: [ReportApi],
  templateUrl: './property-summary.component.html',
  styleUrls: ['./property-summary.component.css']
})
export class PropertySummaryComponent implements OnInit {

  propertyValues: Summary;

  propertyName: string;

  constructor(private reportApi: ReportApi,    private route: ActivatedRoute
  ) { }

  ngOnInit() {
    this.propertyName = this.route.snapshot.params['propertyName'];

    this.reportApi.getPropertyValuesSummary(this.propertyName, 0).subscribe(
      (props) => {
        console.log(props);
        this.propertyValues = props;
      },
      (err) => console.log(err),
      () => { console.log("Downloaded prop values") }
    );
  }

}
