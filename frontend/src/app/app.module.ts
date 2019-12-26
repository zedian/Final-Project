import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule }    from '@angular/forms';
import { AppComponent } from './app.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AppRoutingModule } from './app-routing/app-routing.module';
import { ChatboxComponent } from './chatbox/chatbox.component';
import { HttpClientModule }    from '@angular/common/http';
import { ChatboxService } from './chatbox.service';

import { ScrollToModule } from '@nicky-lenaers/ngx-scroll-to';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    NavbarComponent,
    ChatboxComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule, 
    NgbModule.forRoot(),
    HttpClientModule,
    ScrollToModule.forRoot()
  ],
  providers: [ChatboxService],
  bootstrap: [AppComponent]
})
export class AppModule { }
