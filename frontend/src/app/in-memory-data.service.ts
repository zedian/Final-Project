import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const binary = [
      { id: 0, state: 'Sincere' },
      { id: 1, state: 'Insincere' },
    ];
    return {binary};
  }
}