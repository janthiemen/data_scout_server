import { MenuItem } from "@blueprintjs/core";
import { ItemPredicate, ItemRenderer } from "@blueprintjs/select";
import * as React from "react";

export interface IFilm {
    /** Title of film. */
    title: string;
    /** Release year. */
    year: number;
    /** IMDb ranking. */
    rank: number;
}

/** Top 100 films as rated by IMDb users. http://www.imdb.com/chart/top */
export const TOP_100_FILMS: IFilm[] = [
    { title: "The Shawshank Redemption", year: 1994, rank: 1 },
    { title: "The Godfather", year: 1972, rank: 2 },
    { title: "The Godfather: Part II", year: 1974, rank: 3 },
]

export const renderFilm: ItemRenderer<IFilm> = (film, { handleClick, modifiers, query }) => {
    if (!modifiers.matchesPredicate) {
        return null;
    }
    const text = `${film.rank}. ${film.title}`;
    return (
        <MenuItem
            active={modifiers.active}
            disabled={modifiers.disabled}
            label={film.year.toString()}
            key={film.rank}
            onClick={handleClick}
            text={highlightText(text, query)}
        />
    );
};

export const renderCreateFilmOption = (
    query: string,
    active: boolean,
    handleClick: React.MouseEventHandler<HTMLElement>,
) => (
    <MenuItem
        icon="add"
        text={`Create "${query}"`}
        active={active}
        onClick={handleClick}
        shouldDismissPopover={false}
    />
);

export const filterFilm: ItemPredicate<IFilm> = (query, film, _index, exactMatch) => {
    const normalizedTitle = film.title.toLowerCase();
    const normalizedQuery = query.toLowerCase();

    if (exactMatch) {
        return normalizedTitle === normalizedQuery;
    } else {
        return `${film.rank}. ${normalizedTitle} ${film.year}`.indexOf(normalizedQuery) >= 0;
    }
};

function highlightText(text: string, query: string) {
    let lastIndex = 0;
    const words = query
        .split(/\s+/)
        .filter(word => word.length > 0)
        .map(escapeRegExpChars);
    if (words.length === 0) {
        return [text];
    }
    const regexp = new RegExp(words.join("|"), "gi");
    const tokens: React.ReactNode[] = [];
    while (true) {
        const match = regexp.exec(text);
        if (!match) {
            break;
        }
        const length = match[0].length;
        const before = text.slice(lastIndex, regexp.lastIndex - length);
        if (before.length > 0) {
            tokens.push(before);
        }
        lastIndex = regexp.lastIndex;
        tokens.push(<strong key={lastIndex}>{match[0]}</strong>);
    }
    const rest = text.slice(lastIndex);
    if (rest.length > 0) {
        tokens.push(rest);
    }
    return tokens;
}

function escapeRegExpChars(text: string) {
    return text.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

export const filmSelectProps = {
    itemPredicate: filterFilm,
    itemRenderer: renderFilm,
    items: TOP_100_FILMS,
};

export function createFilm(title: string): IFilm {
    return {
        rank: 100 + Math.floor(Math.random() * 100 + 1),
        title,
        year: new Date().getFullYear(),
    };
}

export function areFilmsEqual(filmA: IFilm, filmB: IFilm) {
    // Compare only the titles (ignoring case) just for simplicity.
    return filmA.title.toLowerCase() === filmB.title.toLowerCase();
}

export function doesFilmEqualQuery(film: IFilm, query: string) {
    return film.title.toLowerCase() === query.toLowerCase();
}

export function arrayContainsFilm(films: IFilm[], filmToFind: IFilm): boolean {
    return films.some((film: IFilm) => film.title === filmToFind.title);
}

export function addFilmToArray(films: IFilm[], filmToAdd: IFilm) {
    return [...films, filmToAdd];
}

export function deleteFilmFromArray(films: IFilm[], filmToDelete: IFilm) {
    return films.filter(film => film !== filmToDelete);
}

export function maybeAddCreatedFilmToArrays(
    items: IFilm[],
    createdItems: IFilm[],
    film: IFilm,
): { createdItems: IFilm[]; items: IFilm[] } {
    const isNewlyCreatedItem = !arrayContainsFilm(items, film);
    return {
        createdItems: isNewlyCreatedItem ? addFilmToArray(createdItems, film) : createdItems,
        // Add a created film to `items` so that the film can be deselected.
        items: isNewlyCreatedItem ? addFilmToArray(items, film) : items,
    };
}

export function maybeDeleteCreatedFilmFromArrays(
    items: IFilm[],
    createdItems: IFilm[],
    film: IFilm,
): { createdItems: IFilm[]; items: IFilm[] } {
    const wasItemCreatedByUser = arrayContainsFilm(createdItems, film);

    // Delete the item if the user manually created it.
    return {
        createdItems: wasItemCreatedByUser ? deleteFilmFromArray(createdItems, film) : createdItems,
        items: wasItemCreatedByUser ? deleteFilmFromArray(items, film) : items,
    };
}