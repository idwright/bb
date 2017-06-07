import { Component, OnInit } from '@angular/core';

import { Entities } from './typescript-angular2-client/model/Entities';
import { Entity } from './typescript-angular2-client/model/Entity';
import { EntityApi } from './typescript-angular2-client/api/EntityApi';
@Component({
selector: 'my-entities',
providers: [ EntityApi ],
templateUrl: './entities.component.html',

})
export class EntitiesComponent  implements OnInit { 

    sourceName: string;

    propertyName: string;
    propertyValue: string;
    
    constructor(private entityApi: EntityApi) { }


    ngOnInit(): void {
    }

}
