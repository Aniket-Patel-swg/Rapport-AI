import React, { useState } from 'react'
import './App.css'
import axios from 'axios'
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

function App() {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const scrapeInternshala = async () => {
    console.log("function called")
    try {
      // Set loading state to true when fetching data
      setLoading(true);
      // Make a GET request to the desired endpoint
      const response = await axios.get('http://127.0.0.1:5000/start_internshala');
      // Set the fetched data to the state
      console.log("Data: ", response.data)
      console.log(typeof (response.data))
      setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      // Update loading state to false after fetching data
      setLoading(false);
    }
  };

  return (
    <>
      <h1>Internshala</h1>
      <div>
        <button onClick={scrapeInternshala} disabled={loading}>
          {loading ? 'Fetching Data...' : 'Fetch Data'}
        </button>
        <br />
        {/* Data:
        {data.map((Internshala, key) => {
          return (
            <>
              <div>
                test
                <h1>{Internshala.company}</h1>
                <h2>{Internshala.skills}</h2>
                <p>{Internshala.link}</p>
              </div></>
          )
        })} */}

        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Job Position</TableCell>
                <TableCell align="right">Company</TableCell>
                <TableCell align="right">Skills</TableCell>
                <TableCell align="right">Link</TableCell>
                <TableCell align="right">Have you applied yet?</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.map((row) => (
                <TableRow
                  key={row.name}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.title}
                  </TableCell>
                  <TableCell align="right">{row.company}</TableCell>
                  <TableCell align="right">{row.skills}</TableCell>
                  <TableCell align="right">
                    <a href={row.link}>Apply here</a>
                    {row.links}</TableCell>
                  <TableCell align="right">
                    <Button variant="contained">Yes</Button>
                    <Button variant="contained" disabled>
                      No
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        {/* {data.map(()=>{
          
        })} */}
      </div>
    </>
  )
}

export default App
