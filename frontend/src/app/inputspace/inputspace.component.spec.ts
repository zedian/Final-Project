import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InputspaceComponent } from './inputspace.component';

describe('InputspaceComponent', () => {
  let component: InputspaceComponent;
  let fixture: ComponentFixture<InputspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InputspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InputspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
