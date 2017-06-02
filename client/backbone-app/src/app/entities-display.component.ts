import { Component, Input, OnInit, OnChanges, SimpleChange } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { Entities } from './typescript-angular2-client/model/Entities';

import { EntityApi } from './typescript-angular2-client/api/EntityApi';

@Component({
  selector: 'entities-display',
  templateUrl: './entities-display.component.html',
  styleUrls: [ './entities-display.component.css' ]
})

export class EntitiesDisplayComponent implements OnInit, OnChanges {

    entities: Entities;

    private _sourceName: string;
    private _propertyName: string;
    private _propertyValue: string;

    @Input()
    set sourceName(sourceName: string) {
        this._sourceName = sourceName;
    }

    get sourceName(): string {
        return this._sourceName;
    }

    @Input()
    set propertyName(propertyName: string) {
        this._propertyName = propertyName;
    }

    get propertyName(): string {
        return this._propertyName;
    }

    @Input()
    set propertyValue(propertyValue: string) {
        this._propertyValue = propertyValue;
    }

    get propertyValue(): string {
        return this._propertyValue;
    }

    constructor(private entityApi: EntityApi,
              private route: ActivatedRoute,
              private location: Location
              ) { 
    }

    ngOnInit(): void {
        console.log("entities display:" + this._sourceName + "/" + this._propertyName);

		this.loadEntities();
    }

	ngOnChanges(changes: {[propKey: string]: SimpleChange}) {
		let log: string[] = [];
		for (let propName in changes) {
		  let changedProp = changes[propName];
		  console.log("Changed:" + JSON.stringify(changedProp));
		}
		this.loadEntities();
	}

    loadEntities(): void {
        if (this._sourceName && this._propertyName && this._propertyValue) {
            this.entityApi.downloadEntitiesByProperty(this._propertyName, this._propertyValue).subscribe(
                (entities) => {
                                console.log(entities);
                                this.entities = entities;
                            },
                            (err) => console.log(err),
                            () => { console.log("Downloaded entities") }
                            );
        }
	}

    goBack(): void {
      this.location.back();
    }

}
