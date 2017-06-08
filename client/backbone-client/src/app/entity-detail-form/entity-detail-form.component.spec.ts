import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EntityDetailFormComponent } from './entity-detail-form.component';

describe('EntityDetailFormComponent', () => {
  let component: EntityDetailFormComponent;
  let fixture: ComponentFixture<EntityDetailFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EntityDetailFormComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EntityDetailFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
