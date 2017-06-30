import { Component, Input, OnInit, ViewChild, TemplateRef, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location } from '@angular/common';

import { Entities } from '../typescript-angular2-client/model/Entities';
import { Entity } from '../typescript-angular2-client/model/Entity';
import { Property } from '../typescript-angular2-client/model/Property';

import { EntityApi } from '../typescript-angular2-client/api/EntityApi';
import { SourceApi } from '../typescript-angular2-client/api/SourceApi';

import { Page } from "../model/page";

@Component({
    selector: 'entities-display',
    templateUrl: './entities-display.component.html',
    styleUrls: ['./entities-display.component.css']
})

export class EntitiesDisplayComponent implements OnInit {

    page: Page = new Page();

    @Input()
    pageSize: number = 1000;

    @Input()
    showRefCount: boolean = false;

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

    @Output()
    sourceChange: EventEmitter<any> = new EventEmitter();
    @Output()
    propertyNameChange: EventEmitter<any> = new EventEmitter();
    @Output()
    propertyValueChange: EventEmitter<any> = new EventEmitter();

    @Input()
    set sourceName(sourceName: string) {
        this._sourceName = sourceName;
        this.sourceChange.emit(this._sourceName);
        this.propertyName = undefined;
        this.page.totalElements = 0;
    }

    get sourceName(): string {
        return this._sourceName;
    }

    @Input()
    set propertyName(propertyName: string) {
        this._propertyName = propertyName;
        this.propertyNameChange.emit(this._propertyName);
        this.propertyValue = undefined;
        this.page.totalElements = 0;

    }

    get propertyName(): string {
        return this._propertyName;
    }

    @Input()
    set propertyValue(propertyValue: string) {
        //console.log('entities-display set propertyValue:' + propertyValue);
        this._propertyValue = propertyValue;
        this.propertyValueChange.emit(this._propertyValue);
        if (this._propertyName && this._propertyValue) {
            this.setPage({ offset: 0, size: this.pageSize });
        }
    }

    get propertyValue(): string {
        return this._propertyValue;
    }

    constructor(private entityApi: EntityApi,
        private sourceApi: SourceApi,
        private route: ActivatedRoute,
        private location: Location,
    ) {
        this.page.pageNumber = 0;
        this.page.size = this.pageSize;
    }

    ngOnInit(): void {
        //console.log("entities display:" + this._sourceName + "/" + this._propertyName);

        console.log("entities-display ngOnInit pageSize:" + this.pageSize);
        //this.setPage({ offset: 0, size: this.pageSize });
    }

    propertyKey(prop: Property) {
        return (prop.source + " " + prop.data_name);
    }

    processEntityResponse(entities) {

        //console.log(entities);

        this.page.totalElements = entities.count;
        this.page.totalPages = this.page.totalElements / this.page.size;
        let start = this.page.pageNumber * this.page.size;
        let end = Math.min((start + this.page.size), this.page.totalElements);

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
            headerTemplate: this.hdrTpl
        };

        if (this.showRefCount) {
            identityCols.push(refsColumn);
        }
        allCols.push(refsColumn);

        entities.fields.forEach(field => {
            let propColumn = {
                'prop': this.propertyKey(field),
                propSource: field.source,
                propName: field.data_name,
                cellTemplate: this.propertyValueTmpl,
                headerTemplate: this.hdrTpl
            };
            allCols.push(propColumn);
        });

        entities.entities.forEach(entity => {
            let entityRow: any = {
                'entityId': entity.entity_id,
                'refs': entity.refs.length
            };

            entity.values.forEach(prop => {
                entityRow[this.propertyKey(prop)] = prop.data_value;
            });
            entityRows.push(entityRow);
        });
        this.rows = entityRows;
        this.columns = allCols;
    }

    loadEntities(): void {
        //console.log("entities-display.loadEntities:" + JSON.stringify(this.page));
        if (this._sourceName && this._propertyName && this._propertyValue) {
            
            this.sourceApi.downloadSourceEntitiesByProperty(this._sourceName, this._propertyName, this._propertyValue, this.page.pageNumber * this.page.size, this.page.size).subscribe(
                (entities) => this.processEntityResponse(entities),
                (err) => console.log(err),
                () => { console.log("Downloaded entities") }
            );
        } else if (this._propertyName && this._propertyValue) {
            this.entityApi.downloadEntitiesByProperty(this._propertyName, this._propertyValue, this.page.pageNumber * this.page.size, this.page.size).subscribe(
                (entities) => this.processEntityResponse(entities),
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

    /**
     * Populate the table with new data based on the page number
     * @param page The page to select
     */
    setPage(pageInfo) {
        console.log("Set page:" + JSON.stringify(pageInfo));
        this.page.pageNumber = pageInfo.offset;
        this.loadEntities();
    }

    goBack(): void {
        this.location.back();
    }

}
