import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SourcePropertySummaryComponent } from './source-property-summary.component';

describe('SourcePropertySummaryComponent', () => {
  let component: SourcePropertySummaryComponent;
  let fixture: ComponentFixture<SourcePropertySummaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SourcePropertySummaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SourcePropertySummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
