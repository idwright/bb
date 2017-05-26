import { Component, OnInit } from '@angular/core';

import { Entities } from './typescript-angular2-client/model/Entities';
import { Entity } from './typescript-angular2-client/model/Entity';
import { EntityApi } from './typescript-angular2-client/api/EntityApi';
@Component({
selector: 'my-entities',
providers: [ EntityApi ],
  template: `<h1>Hello {{name}}</h1>`,

})
export class EntitiesComponent  implements OnInit { 
name = 'Angular';

    entities: Entities;
    selectedEntity: Entity;

    constructor(private entityApi: EntityApi) { }

    getEntities(): void {
    this.entityApi.downloadEntitiesByProperty("sample_type","DNAD").subscribe(response => this.entities = response);
    }

    ngOnInit(): void {
        this.getEntities();
    }

    onSelect(entity: Entity): void {
        this.selectedEntity = entity;
    }
}
