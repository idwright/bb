import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SourceSummaryComponent } from './source-summary.component';

describe('SourceSummaryComponent', () => {
  let component: SourceSummaryComponent;
  let fixture: ComponentFixture<SourceSummaryComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SourceSummaryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SourceSummaryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
