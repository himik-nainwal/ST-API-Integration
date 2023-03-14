import React, { Component, useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { Alertapi } from "./Alertapi";

// class Alertnotifs extends Component {
//   constructor(props) {
//     super(props);
//     this.state = {
//       items: [],
//       isLoaded: false,
//     };
//   }

//   componentDidMount() {
//     fetch("https://dog.ceo/api/breeds/list/all")
//       .then((res) => res.json)
//       .then((json) => {
//         this.setState({
//           isLoaded: true,
//           items: json.items,
//         });
//       });
//   }

  

//   render() {
//     const notify = () => toast.warn('This is an alert !', {
//       position: "top-right",
//       autoClose: 5000,
//       hideProgressBar: false,
//       closeOnClick: true,
//       pauseOnHover: true,
//       draggable: true,
//       progress: undefined,
      
//       });
//     var { isLoaded, items = [] } = this.state;
//     if (!isLoaded) {
//       return <div>Loading.......</div>;
//     } else {
//       return (
//         <div>
//           This page is for notification testing.
//           <h1>API IMAGES</h1>
//           {/* <button className="btnClick">Fetch</button> */}
//           Data has been loaded.
//           <ul>
//             {items.map((item) => (
//               <li key={item.id}>Name: {item.message}</li>
//             ))}
//           </ul>
//           <div>
//             <button onClick={notify}>Notify !</button>
//             <ToastContainer
//               position="top-right"
//               autoClose={5000}
//               hideProgressBar={false}
//               newestOnTop={false}
//               closeOnClick
//               rtl={false}
//               pauseOnFocusLoss
//               draggable
//               pauseOnHover
//             />
//             {/* Same as */}
//             <ToastContainer />
//           </div>
//         </div>
//       );
//     }
//   }
// }

// export default Alertnotifs;


const Alertnotifs = () => {
  const [alert, setAlert] = useState(0)
  const notify = () => toast.warn('This is an alert !', {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      
      });
  useEffect(() => {

    if(alert>Alertapi.length-1){
      return
    }
    notify()
    setTimeout(() => {
      setAlert(alert+1)
    }, 3000);
  }, [alert]);

  return(
    <div>
      {Alertapi.map((data, key) => {
        if(key > alert){return null}
        if(data.success == false){return null}
          return(
            <div>
              
              <ul>
              
                <li>{data.name}  ||  {data.success}  ||  {data.id}</li>

            
              </ul>
            </div>
          )
        
    })}

            <ToastContainer
              position="top-right"
              autoClose={5000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
            />
            
    </div>
  )
}

export default Alertnotifs;


