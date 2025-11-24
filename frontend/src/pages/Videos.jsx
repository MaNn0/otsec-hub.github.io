import React, { useEffect, useState } from "react";
import styled from "styled-components";
import axios from "axios";
import { Link } from "react-router-dom";
import { Container, Row, Col, Card, Button, InputGroup, FormControl, Pagination } from "react-bootstrap";
import { Icon } from "@iconify/react";

import Title from "../components/Title";
import BackToTop from "../components/BackToTop";
import Loading from "../components/Loading";
import { updateTitle } from "../utils";

const StyledSection = styled.section`
  .video-card {
    transition: transform 0.2s;
    &:hover {
      transform: scale(1.02);
    }
  }

  .video-thumbnail {
    height: 200px;
    object-fit: cover;
  }

  .pagination {
    justify-content: center;
  }
`;

const Videos = () => {
  const [videos, setVideos] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [activePage, setActivePage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const videosPerPage = 9;

  const fetchVideos = async (page = 1) => {
    setLoading(true);
    try {
      const res = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/api/get_videos`, {
        params: { page, limit: videosPerPage },
      });
      setVideos(res.data.items || []);
      setTotalPages(Math.ceil(res.data.total / videosPerPage));
      setLoading(false);
    } catch (err) {
      setVideos([]);
      setLoading(false);
    }
  };

  useEffect(() => {
    updateTitle("ICS Videos | OTSec-Hub");
  }, []);

  useEffect(() => {
    fetchVideos(activePage);
  }, [activePage]);

  const getYouTubeVideoId = (url) => {
    try {
      const parsed = new URL(url);
      if (parsed.hostname === "youtu.be") return parsed.pathname.slice(1);
      if (parsed.hostname.includes("youtube.com")) return parsed.searchParams.get("v");
      return null;
    } catch {
      return null;
    }
  };

  const filteredVideos = Array.isArray(videos)
    ? videos.filter(video => video.title.toLowerCase().includes(searchTerm.toLowerCase()))
    : [];

  return (
    <>
      <main>
        <StyledSection className="d-flex flex-column justify-content-center">
          <Container className="d-flex justify-content-center mb-3">
            <Title size="h2" text="ICS Videos" />
          </Container>

          <Container>
            <p className="text-center fs-5 text-muted mb-4">
              Explore the fundamentals of ICS security, PLCs, and common attack vectors. More videos coming soon.
            </p>
            <p className="text-center fs-7 text-muted mb-4">
              Want to contribute? Submit your own ICS/OT security video{" "}
              <Link to="/Resources/Videos/Video-Submission" className="text-primary fw-semibold text-decoration-none">
                here
              </Link>.
            </p>
          </Container>

          <Container className="mb-4 d-flex justify-content-center">
            <InputGroup style={{ maxWidth: "600px" }}>
              <InputGroup.Text id="search">
                <Icon icon="ic:round-search" />
              </InputGroup.Text>
              <FormControl
                placeholder="Search videos by title"
                aria-label="Search videos"
                aria-describedby="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </InputGroup>
          </Container>

          <Container>
            <Row xs={1} md={2} lg={3} className="g-4 justify-content-center">
              {loading ? (
                <Container className="d-flex justify-content-center my-5">
                  <Loading />
                </Container>
              ) : (
                filteredVideos.map((video) => (
                  <Col key={video.id} className="d-flex justify-content-center">
                    <Card className="video-card h-100">
                      <Card.Img
                        variant="top"
                        src={`https://img.youtube.com/vi/${getYouTubeVideoId(video.url)}/sddefault.jpg`}
                        alt={video.title}
                        className="video-thumbnail"
                      />
                      <Card.Body>
                        <Card.Title>{video.title}</Card.Title>
                        <Card.Text>{video.subtitle}</Card.Text>
                        <Link to={`/Resources/Videos/${video.id}`}>
                          <Button className="mt-3" variant="primary">Watch</Button>
                        </Link>
                      </Card.Body>
                    </Card>
                  </Col>
                ))
              )}
            </Row>

            {totalPages > 1 && (
              <Container className="d-flex justify-content-center mt-4">
                <Pagination>
                  <Pagination.Prev
                    onClick={() => setActivePage(prev => Math.max(prev - 1, 1))}
                    disabled={activePage === 1}
                  />
                  {Array.from({ length: totalPages }, (_, i) => (
                    <Pagination.Item
                      key={i + 1}
                      active={i + 1 === activePage}
                      onClick={() => setActivePage(i + 1)}
                    >
                      {i + 1}
                    </Pagination.Item>
                  ))}
                  <Pagination.Next
                    onClick={() => setActivePage(prev => Math.min(prev + 1, totalPages))}
                    disabled={activePage === totalPages}
                  />
                </Pagination>
              </Container>
            )}
          </Container>
        </StyledSection>
      </main>

      <BackToTop home="Home" />
    </>
  );
};

export default Videos;
