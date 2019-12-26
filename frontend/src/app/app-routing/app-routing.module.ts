import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from '../dashboard/dashboard.component';
import { ChatboxComponent } from '../chatbox/chatbox.component';

const routes: Routes = [
  { path: '', component: DashboardComponent },
  { path: 'chatbot', component: ChatboxComponent}
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
