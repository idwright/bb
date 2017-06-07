import { Component, Input, OnInit, OnChanges, SimpleChange, ViewChild, TemplateRef } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import { Entities } from './typescript-angular2-client/model/Entities';

import { EntityApi } from './typescript-angular2-client/api/EntityApi';

@Component({
    selector: 'entities-display',
    templateUrl: './entities-display.component.html',
    styleUrls: ['./entities-display.component.css']
})

export class EntitiesDisplayComponent implements OnInit, OnChanges {

    entities: Entities;

    private _sourceName: string;
    private _propertyName: string;
    private _propertyValue: string;

    rows: any[] = [];
    columns: any[] = [];
    allColumns: any[] = [];


    @ViewChild('hdrTpl') hdrTpl: TemplateRef<any>;
    @ViewChild('identityTmpl') identityTmpl: TemplateRef<any>;
    @ViewChild('propertyValueTmpl') propertyValueTmpl: TemplateRef<any>;

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

    ngOnChanges(changes: { [propKey: string]: SimpleChange }) {
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

                    let entityRows: string[] = [];
                    let identityCols: any[] = [];
                    let allCols: any[] = [];
                    let entityColumn = {
                        'prop': 'entityId',
                        cellTemplate: this.identityTmpl,
                        headerTemplate: this.hdrTpl
                    };
                    allCols.push(entityColumn);
                    identityCols.push(entityColumn);
                    let refsColumn = {
                        'prop': 'refs',
                        'name': 'Associations',
                        cellTemplate: this.identityTmpl,
                        headerTemplate: this.hdrTpl
                    };
                    allCols.push(refsColumn);
                    identityCols.push(refsColumn);
                    entities.forEach(entity => {
                        let entityRow: any = {
                            'entityId': entity.entity_id,
                            'refs': entity.refs.length
                        };

                        entity.values.forEach(prop => {
                            console.log(prop);
                            let propKey = prop.source + "." + prop.data_name;
                            let colIdx: number = -1;
                            for (let i = 0; i < allCols.length; i++) {
                                if (allCols[i].prop == propKey) {
                                    colIdx = i;
                                    break;
                                }
                            }
                            if (colIdx < 0) {
                                let valueColumn = {
                                    'prop': propKey,
                                    propSource: prop.source,
                                    propName: prop.data_name,
                                    cellTemplate: this.propertyValueTmpl,
                                    headerTemplate: this.hdrTpl
                                };
                                allCols.push(valueColumn);
                                if (prop.identity) {
                                    identityCols.push(valueColumn);
                                }
                            }
                            entityRow[propKey] = prop.data_value;

                        });
                        entityRows.push(entityRow);
                    });
                    this.rows = entityRows;
                    this.columns = identityCols;
                },
                (err) => console.log(err),
                () => { console.log("Downloaded entities") }
            );
        }
    }

    toggle(col: any) {
        const isChecked = this.isChecked(col);

        if (isChecked) {
            this.columns = this.columns.filter(c => {
                return c.name !== col.name;
            });
        } else {
            this.columns = [...this.columns, col];
        }
    }

    isChecked(col: any) {
        return this.columns.find(c => {
            return c.name === col.name;
        });
    }

    goBack(): void {
        this.location.back();
    }

}
