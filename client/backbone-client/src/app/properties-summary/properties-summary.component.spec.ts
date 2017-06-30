import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PropertiesSummaryComponent } from './properties-summary.component';

describe('PropertiesSummaryComponent', () => {
  let component: PropertiesSummaryComponent;
  let fixture: ComponentFixture<PropertiesSummaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PropertiesSummaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PropertiesSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
