import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EntitiesDisplayComponent } from './entities-display.component';

describe('EntitiesDisplayComponent', () => {
  let component: EntitiesDisplayComponent;
  let fixture: ComponentFixture<EntitiesDisplayComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EntitiesDisplayComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EntitiesDisplayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
