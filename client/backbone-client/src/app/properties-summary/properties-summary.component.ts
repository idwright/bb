import { Component, OnInit } from '@angular/core';

import { Summary } from '../typescript-angular2-client/model/Summary';
import { ReportApi } from '../typescript-angular2-client/api/ReportApi';

@Component({
  selector: 'app-properties-summary',
  providers: [ ReportApi ],
  templateUrl: './properties-summary.component.html',
  styleUrls: ['./properties-summary.component.css']
})
export class PropertiesSummaryComponent implements OnInit {

	allProperties: Summary;

	constructor(private reportApi: ReportApi) { }

  ngOnInit() {
    			this.reportApi.getPropertiesSummary().subscribe(
				(props) => {
					//console.log(props);
					this.allProperties = props;
				},
				(err) => console.log(err),
				() => { console.log("Downloaded props summary") }
			);
  }

}
