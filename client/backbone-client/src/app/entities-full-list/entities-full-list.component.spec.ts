import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EntitiesFullListComponent } from './entities-full-list.component';

describe('EntitiesFullListComponent', () => {
  let component: EntitiesFullListComponent;
  let fixture: ComponentFixture<EntitiesFullListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EntitiesFullListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EntitiesFullListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
