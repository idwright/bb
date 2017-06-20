import { Component, OnInit } from '@angular/core';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Summary } from '../typescript-angular2-client/model/Summary';
import { ReportApi } from '../typescript-angular2-client/api/ReportApi';

@Component({
selector: 'my-entities',
providers: [ ReportApi ],
templateUrl: './entities.component.html',

})
export class EntitiesComponent implements OnInit, OnChanges { 

    sourceName: string;

    sources: Summary;
    propertyName: string;

    propertyValue: string;
    
    constructor(private reportApi: ReportApi) { }


    ngOnInit(): void {

		 this.reportApi.getSummary()
			 .subscribe(
				 (summary) => {
								 console.log(summary);
								 this.sources = summary;
							 },
				 (err) => console.log(err),
				 () => { console.log("Downloaded summary") }
			 );


    }

}
