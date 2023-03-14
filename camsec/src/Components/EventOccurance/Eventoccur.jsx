import React, { Component } from "react";
import { Eventphotos } from "./Eventphotos";
import { Link } from "react-router-dom";
import {AiOutlineDownload} from "react-icons/all"
class Eventoccur extends Component {
  render() {
    return (
      <div className="events">
        <div className="home">
          <div className="head">
            <div className="heading">
              <div className="head1">HEALTHCARE SEC</div>
              <div className="head2">CAMSEC.AI</div>
            </div>
          </div>

          <hr id="hr" />
        </div>
        <button className="event-btn-alert122"><AiOutlineDownload 
         style={{marginRight:'10px'}} />Download CSV</button>
        <div className="event-page">
        <div className="event-btns">
        <Link to="/Eventoccur1" className="">
        <button className="event-btn-alert">
        Mask Alert
       </button>     </Link>
        <button className="event-btn-alert">Attendance Alert</button>
        <button className="event-btn-alert">Fall Alert</button>
        <button className="event-btn-alert">Fire Alert</button>
        <button className="event-btn-alert">Fight Alert</button>
        <button className="event-btn-alert">Monitoring</button>
        </div>

        <Eventphotos />
        </div>

        


      </div>
    );
  }
}

export default Eventoccur;

// import React from 'react'
// import { useState, useEffect } from 'react'

// function Eventoccur() {

//     const [data, setdata] = useState([]);

// const Eventphoto = () =>{
//     fetch('https://pixabay.com/api/')
//         .then((response) => response.json())
//         .then((json) =>
//         { console.log(json);
//             setdata(json)
//         })
// }

// useEffect(() => {
//     Eventphoto()

// }, []);
//     return (
//         <div>
//             <button onClick={Eventphoto}>Fetch API</button>
//             {/* <pre>{JSON.stringify(data, null, 2)}</pre> */}
//             <div>
//                 <ul>
//                     {data.map((item) => (
//                         <li>{item.image_type}</li>
//                     ))}
//                 </ul>
//             </div>
//         </div>
//     )
// }

// export default Eventoccur

// import React, { Component } from "react";

// class Eventoccur extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       users: [],
//       isLoading: false,
//       isError: false,
//     };
//   }

//   async componentDidMount() {
//     this.setState({ isLoading: true });
//     const response = await fetch("https://jsonplaceholder.typicode.com/users");
//     if (response.ok) {
//       const users = await response.json();
//       this.setState({ users, isLoading: false });
//     } else {
//       this.setState({ isError: true, isLoading: false });
//     }
//   }

//   renderTableHeader = () => {
//     return Object.keys(this.state.users[0]).map(attr => <th key={attr}>{attr.toUpperCase()}</th>)
//   }

//   renderTableRows = () => {
//     return this.state.users.map(user => {
//       return (
//         <tr key={user.id}>
//           <td>{user.id}</td>
//           <td>{user.name}</td>
//           <td>{user.username}</td>
//           <td>{user.email}</td>
//           <td>{`${user.address.street}, ${user.address.city}`}</td>
//           <td>{user.phone}</td>
//           <td>{user.website}</td>
//           <td>{user.company.name}</td>
//         </tr>
//       )
//     })
//   }

//   render() {
//     // if (isLoading) {
//     //   return <div>Loading...</div>;
//     // }

//     // if (isError) {
//     //   return <div>Error</div>;
//     // }
//     return (
//       <div>
//         {/* <div className="home">
//           <div className="head">
//             <div className="heading">
//               <div className="head1">HEALTHCARE SEC</div>
//               <div className="head2">CAMSEC.AI</div>
//             </div>
//           </div>
//           <hr />
//         </div> */}

//         <table>
//           <thead>
//             <tr>{this.renderTableHeader()}</tr>
//           </thead>
//           <tbody>{this.renderTableRows()}</tbody>
//         </table>
//       </div>
//     );
//   }
// }

// export default Eventoccur;
