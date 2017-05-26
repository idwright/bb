import { Component, OnInit } from '@angular/core';

import { EntityImpl } from './model/entityimpl';
import { EntityApi } from './typescript-angular2-client/api/EntityApi';
@Component({
selector: 'my-entities',
providers: [ EntityApi ],
  template: `<h1>Hello {{name}}</h1>`,

})
export class EntitiesComponent  implements OnInit { 
name = 'Angular';

    entities: EntityImpl[];
    selectedEntity: EntityImpl;

    constructor(private entityApi: EntityApi) { }

    getEntities(): void {
    this.entityApi.downloadEntitiesByProperty("sample_type","DNAD").subscribe(response => this.entities = response);
    }

    ngOnInit(): void {
        this.getEntities();
    }

    onSelect(entity: EntityImpl): void {
        this.selectedEntity = entity;
    }
}
