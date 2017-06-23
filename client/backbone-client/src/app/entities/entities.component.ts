import { Component, OnInit } from '@angular/core';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Summary } from '../typescript-angular2-client/model/Summary';
import { ReportApi } from '../typescript-angular2-client/api/ReportApi';

@Component({
	selector: 'my-entities',
	providers: [ReportApi],
	templateUrl: './entities.component.html'
})
export class EntitiesComponent implements OnInit {

	private _source : string;
	sources: Summary;

	sourceProperties: Summary;

	propertyValues: Summary;

    sourceNameSelector: string
	propertyNameSelector: string;
	propertyValueSelector: string;

	constructor(private reportApi: ReportApi) { }


	ngOnInit(): void {

		this.reportApi.getSummary()
			.subscribe(
			(summary) => {
				//console.log(summary);
				this.sources = summary;
			},
			(err) => console.log(err),
			() => { console.log("Downloaded summary") }
			);


	}

	sourceChanged(event) {
		//console.log("Source changed:" + event);
		if (event) {
			this._source = event
			this.reportApi.getPropertiesSummary(event).subscribe(
				(props) => {
					//console.log(props);
					this.sourceProperties = props;
				},
				(err) => console.log(err),
				() => { console.log("Downloaded props summary") }
			);
		} else {
			this.sourceProperties = undefined;
		}
		this.propertyValues = undefined;
	}

	propertyNameChanged(event) {
		//console.log("property name changed:" + event);
		this.propertyNameSelector = event;
		if (event && this._source) {
			this.reportApi.getPropertyValuesSummary(this._source, event).subscribe(
				(props) => {
					console.log(props);
					this.propertyValues = props;
				},
				(err) => console.log(err),
				() => { console.log("Downloaded prop values") }
			);
		} else {
			this.propertyValues = undefined;
		}
	}

	propertyValueChanged(event) {
		//console.log("property value changed:" + event);
		this.propertyValueSelector = event;
	}
}
