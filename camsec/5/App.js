// import { useState } from 'react';
// import Calendar from 'react-calendar';
// import 'react-calendar/dist/Calendar.css';
// import './App.css';

// function App() {
//   const [date, setDate] = useState(new Date());

//   return (
//     <div className='app'>
//       <h1 className='text-center'>React Calendar with Range</h1>
//       <div className='calendar-container'>
//         <Calendar
//           onChange={setDate}
//           value={date}
//           selectRange={true}
//         />
//       </div>
//       {date.length > 0 ? (
//         <p className='text-center'>
//           <span className='bold'>Start:</span>{' '}
//           {date[0].toDateString()}
//           &nbsp;|&nbsp;
//           <span className='bold'>End:</span> {date[1].toDateString()}
//         </p>
//       ) : (
//         <p className='text-center'>
//           <span className='bold'>Default selected date:</span>{' '}
//           {date.toDateString()}
//         </p>
//       )}
//     </div>
//   );
// }

// export default App;
import React from "react";
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Components/Navbar';
import Homepage from './Components/Homepage';
// import Camerasetting from './Components/Camsetting/Camerasetting';
// import Adduser from './Components/Adduser/Adduser';
// import AddImage from "./Components/Adduser/AddImage"
// import Areaselection from './Components/AreaSelection/Areaselection';
// import Eventoccur from './Components/EventOccurance/Eventoccur';
import LoginPage from './Components/LoginPage/LoginPage';
import Alertnotifs from './Components/Alertnotifs/Alertnotifs';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
//import LoginPage from "./Components/LoginPage/LoginPage";
export default function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route exact path="/">
            <LoginPage />
            </Route>
            <Route exact path="/home">
            <Homepage />
            <Navbar/>
           </Route>
           {/* <Route exact path="/addimage">
            <AddImage />
            <Navbar/>
           </Route>
           <Route path="/Camerasetting">
            <Camerasetting />
            <Navbar/>
          </Route>
          <Route path="/Adduser">
           <Navbar/>
            <Adduser />
          </Route>
          <Route path="/Eventoccur">
            <Navbar/>
            <Eventoccur /> 
          </Route>
          <Route path="/Areaselection">
            <Navbar/>
            <Areaselection /> 
          </Route>   */}
        </Switch>
      </div>
    </Router>
  );
}
// You can think of these components as "pages"
// in your app.
