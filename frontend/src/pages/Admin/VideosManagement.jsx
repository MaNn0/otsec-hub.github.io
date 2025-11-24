import React, { useEffect, useState } from "react";
import axios from "axios";
import { useTheme } from 'styled-components'; // Changed from MUI theme
import {
    Box,
    Select,
    MenuItem,
    TextField,
    FormControl,
    InputLabel,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
} from "@mui/material";
import Sidebar from "../../components/Admin/AdminSidebar";
import styled from "styled-components";
import AddVideo from "../../components/Admin/AddVideo";
import { Link } from "react-router-dom";
import EditVideoBtn from "../../components/Admin/EditVideoBtn";
import DeleteBtn from './../../components/Admin/DeleteBtn';
// Simple themed components
const ThemedTableContainer = styled(TableContainer)`
  background-color: ${({ theme }) => theme.name === "light" ? "#f8f9fa" : "#3a3b3c"};
  border-radius: 8px;
`;

const ThemedTableCell = styled(TableCell)`
  color: ${({ theme }) => theme.name === "light" ? "rgba(33, 37, 41, 0.85)" : "rgba(255, 255, 255, 0.8)"} !important;
  border-color: ${({ theme }) => theme.name === "light" ? "#dee2e6" : "#495057"} !important;
`;

const ThemedTableHead = styled(TableHead)`
  background-color: ${({ theme }) => theme.name === "light" ? "#e9ecef" : "#343a40"} !important;
`;

const ThemedTableRow = styled(TableRow)`
    background-color: ${({ theme }) => theme.name === "light" ? "#f8f9fa" : "#3a3b3c"} !important;
`;

const ThemedTypography = styled(Typography)`
color: ${({ theme }) => theme.name === "light" ? "rgba(33, 37, 41, 0.85)" : "rgba(255, 255, 255, 0.8)"} !important;
`;


export default function VideoManagement({ children }) {
    const [videos, setVideos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState("");

    const theme = useTheme();

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/get_videos`);
                setVideos(response.data.items);
                setLoading(false)
            } catch (error) {
                setLoading(true)
            } 
        }
        fetchData();
    }, []);

    const filteredVideos = videos.filter((video) => {
        const matchesSearch =
            video.title.toLowerCase().includes(searchQuery.toLowerCase())
        return matchesSearch;
    });

    function getYouTubeVideoId(url) {
        try {
            const parsed = new URL(url);
            if (parsed.hostname === 'youtu.be') {
                return parsed.pathname.slice(1);
            } else if (
                parsed.hostname === 'www.youtube.com' ||
                parsed.hostname === 'youtube.com'
            ) {
                return parsed.searchParams.get('v');
            }
            return null;
        } catch (err) {
            return null;
        }
    }


    return (
        <Box display="flex" minHeight="100vh" sx={{
            backgroundColor: theme?.name === "light" ? "#ffffff" : "#212529"
        }}>
            <Sidebar />

            <Box flexGrow={1} p={4}>
                {children || (
                    <>
                        <ThemedTypography variant="h5" fontWeight={600} mb={3}>
                            All Videos
                        </ThemedTypography>

                        {loading ? (
                            <Box display="flex" justifyContent="center" mt={5}>
                                <CircularProgress sx={{
                                    color: theme?.name === "light" ? "#28a745" : "#6c757d"
                                }} />
                            </Box>
                        ) : (
                            <>
                                <Box display="flex" gap={2} mb={2} alignItems="center">
                                    <TextField
                                        label="Search by name"
                                        variant="outlined"
                                        size="small"
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        fullWidth
                                        sx={{
                                            '& .MuiInputLabel-root': {
                                                color: theme?.name === "light" ? "#212529" : "#ffffff",
                                            },
                                            '& .MuiOutlinedInput-root': {
                                                '& fieldset': {
                                                    borderColor: theme?.name === "light" ? "#ced4da" : "#6c757d",
                                                },
                                                '&:hover fieldset': {
                                                    borderColor: theme?.name === "light" ? "#adb5bd" : "#495057",
                                                },
                                            },
                                            '& .MuiInputBase-input': {
                                                color: theme?.name === "light" ? "rgba(33, 37, 41, 0.85)" : "rgba(255, 255, 255, 0.8)",
                                            },
                                        }}
                                    />
                                    <AddVideo />
                                </Box>

                                <ThemedTableContainer component={Paper}>
                                    <Table>
                                        <ThemedTableHead>
                                            <TableRow>
                                                <ThemedTableCell align="center">Video</ThemedTableCell>
                                                <ThemedTableCell align="center">Title</ThemedTableCell>
                                                <ThemedTableCell align="center">Subtitle</ThemedTableCell>
                                                <ThemedTableCell align="center">Description</ThemedTableCell>
                                                <ThemedTableCell align="center">Actions</ThemedTableCell>
                                            </TableRow>
                                        </ThemedTableHead>

                                        <TableBody>
                                            {filteredVideos.map((videoData) => (
                                                <ThemedTableRow key={videoData.id} hover>
                                                    <ThemedTableCell align="center">
                                                        <Link to={videoData.url} target="_blank" style={{ textDecoration: 'none' }}>
                                                            <img
                                                                src={`https://img.youtube.com/vi/${getYouTubeVideoId(videoData.url)}/sddefault.jpg`}
                                                                alt={videoData.title}
                                                                style={{ maxHeight: '50px', maxWidth: '100px' }}
                                                            />
                                                        </Link>
                                                    </ThemedTableCell>

                                                    <ThemedTableCell align="center" sx={{
                                                        maxWidth: 200,
                                                        maxHeight: 60,
                                                    }}>{videoData.title}</ThemedTableCell>

                                                    <ThemedTableCell align="center">
                                                        <Box
                                                            sx={{
                                                                maxWidth: 200,
                                                                maxHeight: 60,
                                                                margin: '0 auto',
                                                                overflow: 'auto',
                                                                whiteSpace: 'pre-wrap',
                                                                wordWrap: 'break-word',
                                                            }}
                                                        >
                                                            {videoData.subtitle}
                                                        </Box>
                                                    </ThemedTableCell>

                                                    <ThemedTableCell align="center">
                                                        <Box
                                                            sx={{
                                                                margin: '0 auto',
                                                                maxWidth: 300,
                                                                maxHeight: 100,
                                                                overflow: 'auto',
                                                                whiteSpace: 'pre-wrap',
                                                                wordWrap: 'break-word',
                                                            }}
                                                        >
                                                            {videoData.description}
                                                        </Box>
                                                    </ThemedTableCell>

                                                    <ThemedTableCell align="center">
                                                        <Box display="flex" justifyContent="center" gap={1}>
                                                            <EditVideoBtn video={videoData} />
                                                            <DeleteBtn name="video" id={videoData.id}  />
                                                        </Box>
                                                    </ThemedTableCell>
                                                </ThemedTableRow>
                                            ))}
                                        </TableBody>

                                    </Table>
                                </ThemedTableContainer>
                            </>
                        )}
                    </>
                )}
            </Box>
        </Box>
    );
}