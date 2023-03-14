import React from 'react'
import TableData from "./TableData";
 export function Eventphotos(){

// get table column
 const column = Object.keys(TableData[0]);

 // get table heading data
 const ThData =()=>{
    
     return column.map((data)=>{
         return <th style={{background:'white',color:'black',fontSize:12}} key={data}>{data}</th>
     })
 }

// get table row data
const tdData =() =>{
   
     return TableData.map((data)=>{
       return(
           <tr>
                {
                   column.map((v)=>{
                     if(v=='Image')
                     {
                      return <td style={{borderBottom:'none',borderLeft:'1px solid white',borderRight:'0.2px solid white',display:'flex',justifyContent:'center'}}><img  src='./logo192.png' width='30'></img></td>
                     }
                     else
                     {
                       return <td style={{borderBottom:'none',borderLeft:'1px solid white',borderRight:'0.2px solid white',justifyContent:'center',color:'white'}}>{data[v]}</td>
                     }
                      })
                }
           </tr>
       )
     })
}


  return (
      <table className="table" style={{background: "",marginTop:'2.2vh', color:"white", width:'60%'}} >
        <thead>
         <tr className='mytr'style={{background:'white'  }}>{ThData()}</tr>
        </thead>
        <tbody>{tdData()}</tbody>
       </table>
  )
}
// export default Eventphotos;

// import React from "react";
// // import  {PhotosData}  from "./PhotosData";
// import { PhotosData } from "./PhotosData";
// import { Component, useState, useEffect } from "react";
// import { ToastContainer, toast } from "react-toastify";
// import "react-toastify/dist/ReactToastify.css";

// export const Eventphotos = () => {
//   const [alert, setAlert] = useState(0);
//   const notify = () =>
//     toast.warn("This is an alert !", {
//       position: "top-right",
//       autoClose: 5000,
//       hideProgressBar: false,
//       closeOnClick: true,
//       pauseOnHover: true,
//       draggable: true,
//       progress: undefined,
//     });
//   useEffect(() => {
//     if (alert > PhotosData.length - 1) {
//       return;
//     }
//     notify();
//     setTimeout(() => {
//       setAlert(alert + 1);
//     }, 3000);
//   }, [alert]);

//   return (
//     <div className="table-container">
//       {/* <div className="photos-container">
//         <table className="table-bordered">
//           {PhotosData.map((data, key) => {
//             return (
//               <div>
//                 <thead>
//                   <tr>
//                     <th scope="col">Name</th>
//                     <th scope="col">Image</th>
//                   </tr>
//                 </thead>

//                 <tbody>
//                   <tr>
//                     <td>{data.name}</td>
//                     <td>
//                       <img
//                         src={data.image}
//                         alt=""
//                         height="100px"
//                         width="100px"
//                       />
//                     </td>
//                   </tr>
//                 </tbody>
//               </div>
//             );
//           })}
//         </table>
//       </div> */}
//       {PhotosData.map((data, key) => {
//         if (key > alert) {
//           return null;
//         }
//         if (data.success == false) {
//           return null;
//         }
//         return (
//           <div>
//             <table
//               class="table table-border table-hover-light table-responsive-sm "
//               style={{ color: "white" }}
//             >
//               {/* <thead>
//                 <tr>
//                   <th scope="col">#</th>
//                   <th scope="col">Name</th>
//                   <th scope="col">Image</th>
//                   <th scope="col">Date &amp; Time</th>
//                 </tr>
//               </thead> */}
//               <tbody>
//                 <tr>
//                   {/* <th >1</th> */}
//                   <td id="serial">{data.id}</td>
//                   <td>{data.name}</td>
//                   <td>
//                     {/* <img id="table-img" src={data.image} alt="" height="200px" width="300px" onLoad={Alertnotifs} /> */}
//                     <img
//                       id="table-img"
//                       src={data.image}
//                       alt=""
//                       height="100px"
//                       width="150px"
//                     />
//                   </td>
//                   <td>{data.date_time}</td>
//                 </tr>
//               </tbody>
//             </table>
//           </div>
//         );
//       })}
//       <ToastContainer
//         position="top-right"
//         autoClose={5000}
//         hideProgressBar={false}
//         newestOnTop={false}
//         closeOnClick
//         rtl={false}
//         pauseOnFocusLoss
//         draggable
//         pauseOnHover
//       />
//       )
//     </div>
//   );
// };
